import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { AuthService } from './auth.service';
import { environment } from 'src/environments/environment';

export interface User {
  id: number;
  name: string;
  permissions: Array<{
    name: string;
    valid: boolean;
  }>;
}

@Injectable({
  providedIn: 'root'
})
export class ManageUsersService {

  url = environment.apiServerUrl;

  public items: {[key: number]: User} = {};

  constructor(private auth: AuthService, private http: HttpClient) { }

  getHeaders() {
    const header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Bearer ${this.auth.activeJWT()}`)
    };
    return header;
  }

  getUsers() {
    if (this.auth.can('manage:managers')) {
      this.http.get(this.url + '/managers', this.getHeaders())
      .subscribe((res: any) => {
        this.usersToItems(res.users);
        console.log(res);
      });
    } else if (this.auth.can('manage:baristas')) {
      this.http.get(this.url + '/baristas', this.getHeaders())
      .subscribe((res: any) => {
        this.usersToItems(res.users);
        console.log(res);
      });
    }

  }

  saveUser(user: User) {
    if (this.auth.can('manage:managers')) {
      this.http.patch(this.url + '/managers/' + user.id, user, this.getHeaders())
      .subscribe( (res: any) => {
        console.log(res);
      });
    } else if (this.auth.can('manage:baristas')) {
      this.http.patch(this.url + '/baristas/' + user.id, user, this.getHeaders())
      .subscribe( (res: any) => {
        console.log(res);
      });
    }
  }

  usersToItems(users: Array<User>) {
    for (const user of users) {
      this.items[user.id] = user;
    }
  }
}
