import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import {  UserRecord } from '../types';
import { AuthService } from '../../auth/auth.service';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'app-user-form',
  templateUrl: './usercreate.component.html',
  imports: [FormsModule],
})
export class UserFormComponent {
  userData: UserRecord = {
    name: '',
    username: '',
    email: '',
    password: '',
  };

  constructor(private http: HttpClient, private authService: AuthService, private router: Router) {}

  returnToMain() {
    this.router.navigate(['/users']);
  }

  onSubmit() {

    if (this.authService.storage.getToken()) {
      this.http.post('http://127.0.0.1:8000/user/', this.userData, this.authService.headers()).subscribe(response => {
        console.log(response);
        alert('user successfully created!');
        this.router.navigate(['/users']);
      });
    }
  }
}
