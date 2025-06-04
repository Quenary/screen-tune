import { Component } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { TranslateService } from '@ngx-translate/core';
import { EAppUrls } from '../core/enums/app-urls.enum';
import { AppApiService } from '../core/services/app-api/app-api.service';
import { NewVersionDialogComponent } from '../new-version-dialog/new-version-dialog.component';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { MatIconModule } from '@angular/material/icon';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';

@Component({
  selector: 'app-header',
  imports: [
    TranslateModule,
    MatButtonModule,
    MatMenuModule,
    MatIconModule,
    MatDialogModule,
    MatSnackBarModule,
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
})
export class HeaderComponent {
  constructor(
    private matDialog: MatDialog,
    private matSnackBar: MatSnackBar,
    private translateService: TranslateService,
    private appApiService: AppApiService
  ) {}

  public openRepository() {
    this.appApiService.openExternalUrl(EAppUrls.repo);
  }

  public checkUpdates() {
    this.appApiService.check_latest_release().subscribe((data) => {
      if (!!data?.update_available) {
        const dialogRef = this.matDialog.open(NewVersionDialogComponent, {
          data,
        });
        dialogRef.afterClosed().subscribe((link) => {
          if (!!link) {
            this.appApiService.openExternalUrl(link);
          }
        });
      } else {
        this.matSnackBar.open(
          this.translateService.instant('HEADER.NEW_VERSION_DIALOG.NO_UPDATES'),
          undefined,
          { duration: 1000 }
        );
      }
    });
  }

  public exit() {
    this.appApiService.exit();
  }
}
