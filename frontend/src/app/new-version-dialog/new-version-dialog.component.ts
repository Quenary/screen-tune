import { Component, Inject } from '@angular/core';
import {
  MAT_DIALOG_DATA,
  MatDialogActions,
  MatDialogRef,
  MatDialogTitle,
} from '@angular/material/dialog';
import { IVersionCheckResponse } from '../core/interfaces/version-check';
import { TranslateModule } from '@ngx-translate/core';
import { MatButton } from '@angular/material/button';

@Component({
  selector: 'app-new-version-dialog',
  imports: [TranslateModule, MatDialogTitle, MatDialogActions, MatButton],
  templateUrl: './new-version-dialog.component.html',
  styleUrl: './new-version-dialog.component.scss',
})
export class NewVersionDialogComponent {
  public version: string;

  constructor(
    private dialogRef: MatDialogRef<NewVersionDialogComponent>,
    @Inject(MAT_DIALOG_DATA) private data: IVersionCheckResponse
  ) {
    this.version = data.latest_version;
  }

  public apply() {
    this.dialogRef.close(this.data.latest_release_url);
  }

  public cancel() {
    this.dialogRef.close();
  }
}
