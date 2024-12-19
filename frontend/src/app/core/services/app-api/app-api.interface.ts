import { Observable } from 'rxjs';
import { IConfig, IConfigApplication } from '../../interfaces/config';
import { Injectable } from '@angular/core';
import { IVersionCheckResponse } from '../../interfaces/version-check';

@Injectable()
export abstract class AppApiService {
  /**
   * Get list of display names
   */
  public abstract getDisplayNames(): Observable<string[]>;
  /**
   * Get list of active processes names e.g. ['code.exe', 'chrome.exe']
   */
  public abstract getProcessNames(): Observable<string[]>;
  /**
   * Open external url in system browser
   */
  public abstract openExternalUrl(url: string): Observable<void>;
  /**
   * Get active window process app name e.g. code.exe
   */
  public abstract getActiveWindowProcess(): Observable<string>;
  /**
   * Exit application
   */
  public abstract exit(): Observable<void>;
  /**
   * Get application configuration
   */
  public abstract getConfig(): Observable<IConfig>;
  /**
   * Set application configuration
   */
  public abstract setConfig(config: IConfig): Observable<void>;
  /**
   * Update certain fields of application configuration
   */
  public abstract updateConfig(config: Partial<IConfig>): Observable<void>;
  /**
   * Set application autorun on system startup
   */
  public abstract setAutorun(flag: boolean): Observable<void>;
  /**
   * Get application autorun on system startup
   */
  public abstract getAutorun(): Observable<boolean>;
  /**
   * Get application version
   */
  public abstract getAppVersion(): Observable<string>;
  /**
   * Check for updates
   */
  public abstract check_latest_release(): Observable<IVersionCheckResponse>;
  /**
   * Set live preview active flag
   * @param active
   */
  public abstract setLivePreviewActive(active: boolean): Observable<void>;
  /**
   * Set application live preview values
   * @param values
   */
  public abstract setLivePreviewValues(
    values: IConfigApplication
  ): Observable<void>;
}
