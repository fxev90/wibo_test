import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { UsersComponent } from './users/users.component';
import { authGuard } from './auth/auth.guard';
import { CatsComponent } from './cats/cats.component';
import { CatsFormComponent } from './cats/create/catcreate.component';

export const routes: Routes = [
    { path: '', redirectTo: '/login', pathMatch: 'full' },
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterComponent, },
    { path: 'users', component: UsersComponent },
    { path: 'cats', component: CatsComponent },
    { path: 'cats/create', component: CatsFormComponent }
];