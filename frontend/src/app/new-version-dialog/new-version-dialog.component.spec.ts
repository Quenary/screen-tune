import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewVersionDialogComponent } from './new-version-dialog.component';

describe('NewVersionDialogComponent', () => {
  let component: NewVersionDialogComponent;
  let fixture: ComponentFixture<NewVersionDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NewVersionDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NewVersionDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
