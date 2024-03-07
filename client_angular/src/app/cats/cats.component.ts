import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { CatRecord } from './types';

@Component({
  selector: 'app-cats',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cats.component.html',
  styleUrl: './cats.component.css'
})
export class CatsComponent {
  catList: CatRecord[] = []
  constructor(private http: HttpClient, private authService: AuthService, private router: Router) {
  }

  navigateToCreate() {
    this.router.navigate(['/cats/create']);
  }

  navigateToUsers() {
    this.router.navigate(['/users/']);
  }

  onCatRemove(id: string) {
    this.http.delete('http://127.0.0.1:8000/cats/' + id, this.authService.headers()).subscribe(response => {
      console.log(response);
      alert(` Cat ${id} deleted! `);
      this.loadCats();
    })
  }

  loadCats() {
    if (this.authService.storage.getToken()) {
      this.http.get<CatRecord[]>('http://127.0.0.1:8000/cats/', this.authService.headers()).subscribe(response => {
        console.log(response);
        this.catList = response;
      })
    }
  }

  ngOnInit() {
    this.loadCats();
  }
}
