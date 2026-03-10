use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use wasm_bindgen::prelude::*;
use wasm_bindgen_futures::spawn_local;
use web_sys::{window, HtmlElement, HtmlInputElement};

#[derive(Serialize)]
pub struct ChatRequest {
    pub query: String,
}

#[derive(Deserialize, Debug, Clone)]
pub struct ChatResponse {
    pub answer: String,
    pub metadata: Option<HashMap<String, String>>,
}

async fn fetch_ai_response(query: &str) -> Result<ChatResponse, JsValue> {
    let client = reqwest::Client::new();
    let request_body = ChatRequest {
        query: query.to_string(),
    };

    let res = client
        .post("http://localhost:9911/api/chat")
        .json(&request_body)
        .send()
        .await
        .map_err(|e| JsValue::from_str(&format!("Reqwest error: {:?}", e)))?;

    let chat_data: ChatResponse = res
        .json()
        .await
        .map_err(|e| JsValue::from_str(&format!("JSON Parse error: {:?}", e)))?;

    Ok(chat_data)
}

#[wasm_bindgen(start)]
pub fn run() -> Result<(), JsValue> {
    let window = window().expect("no global `window` exists");
    let document = window.document().expect("should have a document on window");

    let root = document
        .get_element_by_id("wasm-portfolio-root")
        .unwrap_or_else(|| {
            let div = document.create_element("div").unwrap();
            div.set_id("wasm-portfolio-root");
            document.body().unwrap().append_child(&div).unwrap();
            div
        });

    root.set_inner_html(
        r#"
        <style>
            #wasm-portfolio-root { font-family: sans-serif; height: 100vh; margin: 0; display: flex; flex-direction: column; }
            .header { background: #111827; color: white; padding: 1rem; text-align: center; font-weight: bold; }
            .split-container { display: flex; flex: 1; overflow: hidden; }
            .chat-pane { flex: 1; padding: 1.5rem; display: flex; flex-direction: column; border-right: 2px solid #e5e7eb; background: #ffffff; }
            .meta-pane { flex: 1; padding: 1.5rem; background: #f9fafb; overflow-y: auto; }
            .input-group { display: flex; margin-top: 1rem; }
            #chat-input { flex: 1; padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 0.375rem 0 0 0.375rem; font-size: 1rem; }
            #send-btn { background: #3b82f6; color: white; border: none; padding: 0.75rem 1.5rem; cursor: pointer; border-radius: 0 0.375rem 0.375rem 0; font-weight: bold; }
            #send-btn:hover { background: #2563eb; }
            #chat-history { flex: 1; overflow-y: auto; border: 1px solid #e5e7eb; padding: 1rem; border-radius: 0.375rem; background: #f3f4f6; white-space: pre-wrap; margin-bottom: 1rem;}
            .meta-card { background: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .tag { display: inline-block; background: #e0e7ff; color: #3730a3; padding: 0.25rem 0.5rem; border-radius: 9999px; font-size: 0.875rem; margin: 0.25rem; }
        </style>
        <div class="header">Edmond's AI Agent & Portfolio Explorer</div>
        <div class="split-container">
            <div class="chat-pane">
                <h3>Ask AI Agent</h3>
                <div id="chat-history">Hello! I am Edmond's AI assistant. Ask me about his projects, skills, or specific tech stacks!</div>
                <div class="input-group">
                    <input type="text" id="chat-input" placeholder="e.g. Tell me about the Solana Lending Pool..." />
                    <button id="send-btn">Send</button>
                </div>
            </div>
            <div class="meta-pane">
                <h3>Relevant Portfolio Metadata</h3>
                <div id="meta-content" class="meta-card">
                    <p style="color: #6b7280; font-style: italic;">Ask a question to see the matching project details here.</p>
                </div>
            </div>
        </div>
        "#,
    );

    let btn = document.get_element_by_id("send-btn").unwrap().dyn_into::<HtmlElement>().unwrap();
    let input = document.get_element_by_id("chat-input").unwrap().dyn_into::<HtmlInputElement>().unwrap();

    let input_clone = input.clone();
    let document_clone = document.clone();
    
    let closure = Closure::wrap(Box::new(move || {
        let query = input_clone.value();
        if query.trim().is_empty() { return; }

        let doc = document_clone.clone();
        let history_div = doc.get_element_by_id("chat-history").unwrap();
        let meta_div = doc.get_element_by_id("meta-content").unwrap();

        let current_history = history_div.inner_html();
        history_div.set_inner_html(&format!("{}<br><br><b>You:</b> {}<br><b>AI:</b> <i>Thinking...</i>", current_history, query));
        meta_div.set_inner_html("<i>Searching vector database...</i>");
        input_clone.set_value("");

        spawn_local(async move {
            match fetch_ai_response(&query).await {
                Ok(response) => {
                    history_div.set_inner_html(&format!("{}<br><br><b>You:</b> {}<br><b>AI:</b> {}", current_history, query, response.answer));
                    
                    if let Some(meta) = response.metadata {
                        if meta.is_empty() {
                            meta_div.set_inner_html("<p>No specific project metadata found for this query.</p>");
                        } else {
                            let mut html = String::from("");
                            
                            if let Some(proj) = meta.get("project") {
                                html.push_str(&format!("<h2 style='margin-top:0; color:#1f2937;'>{}</h2>", proj));
                            }
                            if let Some(link) = meta.get("link") {
                                html.push_str(&format!("<p><a href='{}' target='_blank' style='color:#2563eb; text-decoration:none;'>View on GitHub / Web</a></p>", link));
                            }
                            
                            if let Some(domain) = meta.get("domain") { html.push_str(&format!("<span class='tag' style='background:#fef3c7; color:#92400e;'>{}</span>", domain)); }
                            if let Some(category) = meta.get("category") { html.push_str(&format!("<span class='tag' style='background:#dcfce7; color:#166534;'>{}</span>", category)); }
                            
                            if let Some(tech) = meta.get("tech_stack") {
                                html.push_str("<h4 style='margin-bottom:0.5rem;'>Tech Stack</h4><div>");
                                for t in tech.split(',') {
                                    html.push_str(&format!("<span class='tag'>{}</span>", t.trim()));
                                }
                                html.push_str("</div>");
                            }

                            if let Some(achieve) = meta.get("key_achievement") { html.push_str(&format!("<h4>Key Achievement</h4><p>{}</p>", achieve)); }
                            if let Some(challenge) = meta.get("challenge") { html.push_str(&format!("<h4>Challenge Overcome</h4><p>{}</p>", challenge)); }

                            meta_div.set_inner_html(&html);
                        }
                    } else {
                        meta_div.set_inner_html("<p>No project metadata retrieved.</p>");
                    }
                }
                Err(_e) => {
                    history_div.set_inner_html(&format!("{}<br><br><b>Error:</b> Could not connect to the server.", current_history));
                    meta_div.set_inner_html("<p style='color:red;'>Connection to backend failed. Is FastAPI running on port 9911?</p>");
                }
            }
        });
    }) as Box<dyn FnMut()>);

    btn.add_event_listener_with_callback("click", closure.as_ref().unchecked_ref()).unwrap();
    closure.forget();

    Ok(())
}