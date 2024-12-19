import { Injectable } from '@angular/core';
import { AppApiService } from './app-api.interface';
import { from, Observable, of } from 'rxjs';
import { IPyWebViewApi } from '../../interfaces/pywebview';
import { IConfig, IConfigApplication } from '../../interfaces/config';
import { isPywebview } from '../../decorators/is-pywebview.decorator';
import { IVersionCheckResponse } from '../../interfaces/version-check';

@Injectable()
export class PywebviewApiService extends AppApiService {
  protected get api(): IPyWebViewApi {
    return window.pywebview.api;
  }

  @isPywebview(() => of(['DISPLAY_1', 'DISPLAY_2']))
  public override getDisplayNames(): Observable<string[]> {
    return from(this.api.get_display_names());
  }

  @isPywebview(() => of(['code.exe', 'notepad.exe']))
  public override getProcessNames(): Observable<string[]> {
    return from(this.api.get_process_names());
  }

  @isPywebview(() => of(null))
  public override openExternalUrl(url: string): Observable<void> {
    return from(this.api.open_external_url(url));
  }

  @isPywebview(() => of(null))
  public override exit(): Observable<void> {
    return from(this.api.exit());
  }

  @isPywebview(() => of(null))
  public override getActiveWindowProcess(): Observable<string> {
    return from(this.api.get_active_window_process());
  }

  @isPywebview(() =>
    of(<IConfig>{
      checkUpdates: true,
      launchMinimized: false,
      displays: [],
      applications: {},
    })
  )
  public override getConfig(): Observable<IConfig> {
    return from(this.api.get_config());
  }

  @isPywebview(() => of(null))
  public override setConfig(config: IConfig): Observable<void> {
    return from(this.api.set_config(config));
  }

  @isPywebview(() => of(null))
  public override updateConfig(config: Partial<IConfig>): Observable<void> {
    return from(this.api.update_config(config));
  }

  @isPywebview(() => of(null))
  public override setAutorun(flag: boolean): Observable<void> {
    return from(this.api.set_autorun(flag));
  }

  @isPywebview(() => of(false))
  public override getAutorun(): Observable<boolean> {
    return from(this.api.get_autorun());
  }

  @isPywebview(() => of('0.0.0'))
  public override getAppVersion(): Observable<string> {
    return from(this.api.get_app_version());
  }

  @isPywebview(() => of(null))
  public override check_latest_release(): Observable<IVersionCheckResponse> {
    return from(this.api.check_latest_release());
  }

  @isPywebview(() => of(null))
  public override setLivePreviewActive(active: boolean): Observable<void> {
    return from(this.api.set_live_preview_active(active));
  }

  @isPywebview(() => of(null))
  public override setLivePreviewValues(
    values: IConfigApplication
  ): Observable<void> {
    return from(this.api.set_live_preview_values(values));
  }
}
