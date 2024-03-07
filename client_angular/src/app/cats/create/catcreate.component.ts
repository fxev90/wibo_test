import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CatRecord } from '../types';
import { AuthService } from '../../auth/auth.service';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'app-cats-form',
  templateUrl: './catcreate.component.html',
  imports: [FormsModule],
})
export class CatsFormComponent {
  catData: CatRecord = {
    name: '',
    breed: '',
    age: 0,
    gender: '',
    status: '',
    description: '',
    id: ''
  };

  constructor(private http: HttpClient, private authService: AuthService, private router: Router) {}

  returnToMain() {
    this.router.navigate(['/cats']);
  }

  onSubmit() {

    if (this.authService.storage.getToken()) {
      this.http.post('http://127.0.0.1:8000/cats/', this.catData, this.authService.headers()).subscribe(response => {
        console.log(response);
        alert('cats successfully created!');
        this.router.navigate(['/cats']);
      });
    }
  }
}
