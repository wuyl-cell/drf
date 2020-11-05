<template>
    <div>
        <Header></Header>
        <Banner></Banner>
        <Footer></Footer>
    </div>
</template>

<script>
import Header from "./common/Header";
import Banner from "./common/Banner";
import Footter from "./common/Footter";

export default {
    name: "Home",
    components:{
        Header: Header,
        Banner: Banner,
        Footer: Footter,
    }
}
</script>

<style scoped>

</style>
