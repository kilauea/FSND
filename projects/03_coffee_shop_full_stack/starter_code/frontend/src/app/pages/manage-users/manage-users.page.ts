import { Component, OnInit } from '@angular/core';
import { ManageUsersService, User } from '../../services/manage.users.service';
import { ModalController } from '@ionic/angular';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-manage-users',
  templateUrl: './manage-users.page.html',
  styleUrls: ['./manage-users.page.scss'],
})
export class ManageUsersPage implements OnInit {
  Object = Object;

  constructor(
    public auth: AuthService,
    private modalCtrl: ModalController,
    public users: ManageUsersService
    ) {
    this.users.getUsers();
  }

  ngOnInit() {
    
  }

  updatePermission(event, userId: number, permission: number) {
    this.users.items[userId].permissions[permission].valid = event.target.checked
    console.log('Nuevo estado: ' + this.users.items[userId].permissions[permission].name + " - " + event.target.checked);
  }

  saveClicked(userId) {
    this.users.saveUser(this.users.items[userId]);
  }

  // async openForm(activedrink: User = null) {
  //   if (!this.auth.can('get:drinks-detail')) {
  //     return;
  //   }

  //   const modal = await this.modalCtrl.create({
  //     component: DrinkFormComponent,
  //     componentProps: { drink: activedrink, isNew: !activedrink }
  //   });

  //   modal.present();
  // }

}
