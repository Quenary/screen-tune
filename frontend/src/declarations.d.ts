import { IConfig } from './app/core/interfaces/config';

declare global {
  interface Window {
    pywebview: IPyWebView;
  }
}
