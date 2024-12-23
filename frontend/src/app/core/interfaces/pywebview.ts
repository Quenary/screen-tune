import { IConfig, IConfigApplication } from './config';
import { IVersionCheckResponse } from './version-check';

export type TPywebviewApi = {
  /**
   * Call python api method
   * @param method method name
   */
  invoke(method: string): Promise<any>;
  invoke(method: 'get_display_names'): Promise<string[]>;
  invoke(method: 'get_process_names'): Promise<string[]>;
  invoke(method: 'open_external_url', url: string): Promise<void>;
  invoke(method: 'exit'): Promise<void>;
  invoke(method: 'get_active_window_process'): Promise<string>;
  invoke(method: 'get_config'): Promise<IConfig>;
  invoke(method: 'set_config', config: IConfig): Promise<void>;
  invoke(method: 'update_config', config: Partial<IConfig>): Promise<void>;
  invoke(method: 'set_autorun', flag: boolean): Promise<void>;
  invoke(method: 'get_autorun'): Promise<boolean>;
  invoke(method: 'get_app_version'): Promise<string>;
  invoke(method: 'check_latest_release'): Promise<IVersionCheckResponse>;
  invoke(method: 'set_live_preview_active', active: boolean): Promise<void>;
  invoke(
    method: 'set_live_preview_values',
    values: IConfigApplication
  ): Promise<void>;
};
