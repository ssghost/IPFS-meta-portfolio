/* @ts-self-types="./ipfs_meta_portfolio.d.ts" */

import * as wasm from "./ipfs_meta_portfolio_bg.wasm";
import { __wbg_set_wasm } from "./ipfs_meta_portfolio_bg.js";
__wbg_set_wasm(wasm);
wasm.__wbindgen_start();
export {
    run
} from "./ipfs_meta_portfolio_bg.js";
