import { IConfig } from './app/core/interfaces/config';
import { IPyWebView } from './app/core/interfaces/pywebview';

declare global {
  interface Window {
    pywebview: IPyWebView;
  }
}
