import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  name: string = '';
  username: string = '';
  email: string = '';
  password: string = '';

  constructor(private http: HttpClient, private router: Router) { }

  redirectToLogin() {
    this.router.navigate(['/login']);
  }


  submitForm() {
    const formData = {
      name: this.name,
      username: this.username,
      email: this.email,
      password: this.password,
    };


    this.http.post('http://127.0.0.1:8000/user/', formData)
      .subscribe(response => {
        // Handle the response as needed
        console.log(response);
        this.router.navigate(['/login']);
      }, error => {
        // Handle errors
        console.error(error);
      });
  }
}