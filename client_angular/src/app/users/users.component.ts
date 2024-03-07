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

  
  loadUsers() {
    if (this.authService.storage.getToken()) {
      this.http.get<UserRecord[]>('http://127.0.0.1:8000/user/', this.authService.headers()).subscribe(response => {
        console.log(response);
        this.userList = response;
      })
    }
  }

  onUserRemove(id: string) {
    this.http.delete('http://127.0.0.1:8000/user/' + id, this.authService.headers()).subscribe(response => {
      console.log(response);
      alert(` User ${id} deleted! `);
      this.loadUsers();
    })
  }

  ngOnInit() {
    if (this.authService.storage.getToken()) {
      this.loadUsers();
    }
  }
  navigateToCreate() {
    this.router.navigate(['/users/create']);
  }

  navigateToCats() {
    this.router.navigate(['/cats/']);
  }
}
