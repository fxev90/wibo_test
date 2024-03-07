import { HttpClient } from '@angular/common/http';
import { AuthService } from './../auth/auth.service';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

interface UserRecord {
  name: string;
  username: string;
  email: string;
  id: string;
}

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './users.component.html',
  styleUrl: './users.component.css'
})
export class UsersComponent {
  userList: UserRecord[] = []
  constructor(private http: HttpClient, private authService: AuthService, private router: Router) {
  }

  ngOnInit() {
    if (this.authService.storage.getToken()) {
      this.http.get<UserRecord[]>('http://127.0.0.1:8000/user/', this.authService.headers()).subscribe(response => {
        console.log(response);
        this.userList = response;
      })
    }
  }
}
