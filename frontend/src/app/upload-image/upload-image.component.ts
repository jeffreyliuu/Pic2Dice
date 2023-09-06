import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-upload-image',
  templateUrl: './upload-image.component.html',
  styleUrls: ['./upload-image.component.css']
})

export class UploadImageComponent {
  outputUrl!: string;
  selectedFile!: File;

  constructor(private http: HttpClient) { }

  onFileSelected(event: Event) {
    const target = event.target as HTMLInputElement;
    const file: File = (target.files as FileList)[0];
    this.selectedFile = file;
  }
  

  uploadImage() {
    const fd = new FormData();
    fd.append('file', this.selectedFile, this.selectedFile.name);
    this.http.post<any>('http://localhost:5000/upload', fd).subscribe(res => {
      this.outputUrl = res['url'];
    });
  }
}