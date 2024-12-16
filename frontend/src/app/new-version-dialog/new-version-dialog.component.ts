import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { IVersionCheckResponse } from '../core/interfaces/version-check';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-new-version-dialog',
  imports: [
    TranslateModule,
  ],
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
