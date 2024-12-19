import { IConfig, IConfigApplication } from './config';
import { IVersionCheckResponse } from './version-check';

export interface IPyWebView {
  api: IPyWebViewApi;
}
export interface IPyWebViewApi {
  get_display_names: () => Promise<string[]>;
  get_process_names: () => Promise<string[]>;
  open_external_url: (url: string) => Promise<void>;
  exit: () => Promise<void>;
  get_active_window_process: () => Promise<string>;
  get_config: () => Promise<IConfig>;
  set_config: (config: IConfig) => Promise<void>;
  update_config: (config: Partial<IConfig>) => Promise<void>;
  set_autorun: (flag: boolean) => Promise<void>;
  get_autorun: () => Promise<boolean>;
  get_app_version: () => Promise<string>;
  check_latest_release: () => Promise<IVersionCheckResponse>;
  set_live_preview_active: (active: boolean) => Promise<void>;
  set_live_preview_values: (values: IConfigApplication) => Promise<void>;
}
