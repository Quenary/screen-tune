import {
  ApplicationConfig,
  EnvironmentInjector,
  importProvidersFrom,
  inject,
  provideAppInitializer,
  provideZoneChangeDetection,
} from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import {
  TranslateLoader,
  TranslateModule,
  TranslateService,
} from '@ngx-translate/core';
import { LOCATION_INITIALIZED } from '@angular/common';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { HttpClient, provideHttpClient } from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { AppApiService } from './core/services/app-api/app-api.service';
import { PywebviewApiService } from './core/services/app-api/pywebview-api.service';

function TranslateInitializerFactory(environmentInjector: EnvironmentInjector) {
  return new Promise<any>((resolve: any) => {
    const locationInitialized = environmentInjector.get(
      LOCATION_INITIALIZED,
      Promise.resolve(null)
    );
    const translateService = environmentInjector.get(TranslateService);
    locationInitialized.then(() => {
      const langToSet = 'ru';
      translateService.setDefaultLang(langToSet);
      translateService.use(langToSet).subscribe({
        complete: () => resolve(null),
      });
    });
  });
}

function HttpLoaderFactory(httpClient: HttpClient) {
  return new TranslateHttpLoader(httpClient, '../i18n/', '.json');
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(),
    importProvidersFrom(
      TranslateModule.forRoot({
        loader: {
          provide: TranslateLoader,
          useFactory: HttpLoaderFactory,
          deps: [HttpClient],
        },
      })
    ),
    provideAppInitializer(() =>
      TranslateInitializerFactory(inject(EnvironmentInjector))
    ),
    provideAnimationsAsync(),
    {
      provide: AppApiService,
      useClass: PywebviewApiService,
    },
  ],
};
