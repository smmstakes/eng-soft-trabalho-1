<template>
    <div class="main">
        <TopBar/>
        <div class="center-text">
            <h1>Olá, {{ name }}</h1>
            <p>Ainda não tem nada por aqui, você gostaria de:</p>
            
            <div class="choose-mode-buttons">
                <button class="create-project">+ Criar um Projeto</button>
                <button class="join-project"> Ingressar em um Projeto</button>
            </div>
        </div>
    </div>
</template>

<script setup>
// TODO: Receber nome vindo da API depois
const name = "Fulano"
</script>

<style scoped>

.main {
    display:flex;
    flex-direction: column;

    height: 100%;
    width: 100%;
}

.center-text {
    display: flex;
    flex-direction: column;

    /* align-items: flex-start; */
    /* align-self: center; */
    justify-self: center;

    margin: 120px 0px 0px 20%;
    width: 400px;
    /* font-size: large; */
}

.center-text h1 {
    font-weight: 400;
    font-size: 38px;
    margin: 5px 0px;
}

.center-text p {
    color: #525252;
    font-size: 25px;
    margin: 20px 0px;
}

.choose-mode-buttons {
    display:flex;
    justify-content: space-between;

    width: 100%;
}

.choose-mode-buttons button {
    background-color: #171717;
    color: white;
    font-weight: 400;

    height: 40px;
    padding: 0px 30px;
    border: none;
    border-radius: 6px;
}

.choose-mode-buttons button:hover {
    color: black;
    transition-duration: 500ms;
    background-color: #FFFF;
    border: 1px solid #D4D4D4;

    cursor: pointer;
}


</style>