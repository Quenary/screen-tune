import { Injectable } from '@angular/core';
import { AppApiService } from './app-api.service';
import {
  from,
  fromEvent,
  map,
  Observable,
  of,
  shareReplay,
  take,
  timeout,
} from 'rxjs';
import { TPywebviewApi } from '../../interfaces/pywebview';
import { IConfig, IConfigApplication } from '../../interfaces/config';
import { isPywebview } from '../../decorators/is-pywebview.decorator';
import { IVersionCheckResponse } from '../../interfaces/version-check';

@Injectable()
export class PywebviewApiService extends AppApiService {
  public readonly isApiReady$ = fromEvent(window, 'isApiReady').pipe(
    map(() => true),
    timeout({ each: 1000, with: () => of(true) }),
    take(1),
    shareReplay(1)
  );

  protected get api():TPywebviewApi {
    return window.pywebview.api;
  }

  @isPywebview(() => of(['DISPLAY_1', 'DISPLAY_2']))
  public override getDisplayNames(): Observable<string[]> {
    return from(this.api.invoke('get_display_names'));
  }

  @isPywebview(() => of(['code.exe', 'notepad.exe']))
  public override getProcessNames(): Observable<string[]> {
    return from(this.api.invoke('get_process_names'));
  }

  @isPywebview(() => of(null))
  public override openExternalUrl(url: string): Observable<void> {
    return from(this.api.invoke('open_external_url', url));
  }

  @isPywebview(() => of(null))
  public override exit(): Observable<void> {
    return from(this.api.invoke('exit'));
  }

  @isPywebview(() => of(null))
  public override getActiveWindowProcess(): Observable<string> {
    return from(this.api.invoke('get_active_window_process'));
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
    return from(this.api.invoke('get_config'));
  }

  @isPywebview(() => of(null))
  public override setConfig(config: IConfig): Observable<void> {
    return from(this.api.invoke('set_config', config));
  }

  @isPywebview(() => of(null))
  public override updateConfig(config: Partial<IConfig>): Observable<void> {
    return from(this.api.invoke('update_config', config));
  }

  @isPywebview(() => of(null))
  public override setAutorun(flag: boolean): Observable<void> {
    return from(this.api.invoke('set_autorun', flag));
  }

  @isPywebview(() => of(false))
  public override getAutorun(): Observable<boolean> {
    return from(this.api.invoke('get_autorun'));
  }

  @isPywebview(() => of('0.0.0'))
  public override getAppVersion(): Observable<string> {
    return from(this.api.invoke('get_app_version'));
  }

  @isPywebview(() => of(null))
  public override check_latest_release(): Observable<IVersionCheckResponse> {
    return from(this.api.invoke('check_latest_release'));
  }

  @isPywebview(() => of(null))
  public override setLivePreviewActive(active: boolean): Observable<void> {
    return from(this.api.invoke('set_live_preview_active', active));
  }

  @isPywebview(() => of(null))
  public override setLivePreviewValues(
    values: IConfigApplication
  ): Observable<void> {
    return from(this.api.invoke('set_live_preview_values', values));
  }
}
