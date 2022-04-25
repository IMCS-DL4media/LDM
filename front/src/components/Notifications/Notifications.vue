<template>
  <div class="row" >
    <div class="col-sm-4 offset-sm-7" style="position: absolute;z-index:99;">
      <div v-if="notifications.length > 4" class="alert alert-dismissible fade show alert-warning" @click="removeAllNotifications()"> 
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        Remove all notifications
      </div>
      <div v-for="notification in notifications" :id="notification.id">
        <div class="alert alert-dismissible fade show" :class="notification.type" @click="removeNotification(notifications, notification.id)">
          <button type="button" class="close" data-dismiss="alert">&times;</button>
          {{notification.msg}}
        </div>
      </div>
    </div>
  </div>
</template>

<script src="./Notifications.js"></script>
