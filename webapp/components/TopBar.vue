<template>
    <div class="top-bar">
        <div class="app-title">
            <img src="../public/logo.svg" alt="Logo do sistema">
            <h3>Sistema Scrum</h3>
        </div>
        <a class="profile">
            <img src="" alt="">
        </a>
    </div>
</template>

<style scoped>
.top-bar {
    /* position: fixed; */
    width: 100%;
    height: 65px;
    display: flex;

    align-items: center;
    justify-content: space-between;
    border-bottom: 2.5px solid #E5E5E5;

}

.top-bar img {
    margin: 0px 25px;
}

.top-bar h3 {
    font-weight: 400;
}

.top-bar .app-title {
    display: flex;
}

.top-bar .profile {
    width: 40px;
    height: 40px;
    background-color: #4caf50;
    border-radius: 50%;


    margin-right: 25px;
}
</style>