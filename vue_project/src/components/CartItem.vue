<template>
    <div class="cart_item">
        <div class="cart_column column_1">
            <el-checkbox class="my_el_checkbox" v-model="course.selected"></el-checkbox>
        </div>
        <div class="cart_column column_2">
            <img :src="course.course_img" alt="">
            <span><router-link :to="'/detail/' + course.id">{{ course.name }}</router-link></span>
        </div>
        <div class="cart_column column_3">
            <el-select v-model="course.expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select">
                <el-option :label="expire.expire_text" :value="expire.expire_id" :key="expire.expire_id"
                           v-for="expire in course.expire_list"></el-option>
            </el-select>
        </div>
        <div class="cart_column column_4" v-for="expire in course.expire_list" v-if="expire.expire_id == expire_time">
            ¥{{ expire.price }}
        </div>
        <div class="cart_column column_4" @click="del_CartItem">
            <button>删除</button>
        </div>
    </div>
</template>

<script>
export default {
    name: "CartItem",
    data() {
        return {
            course_id: this.course.id,
            expire_time: this.course.expire_id,
        }
    },
    methods: {
        check_user_login() {
            let token = sessionStorage.getItem('token')
            if (token) {
                return token
            } else {
                let self = this
                this.$confirm('请登陆后在添加购物车', {
                    callback() {
                        self.$router.push("/login")
                    }
                })
                return false
            }
        },
        del_CartItem() {
            let token = this.check_user_login()
            this.$axios({
                url: this.$settings.HOST + 'cart/option/',
                method: 'delete',
                data: {
                    course_id: this.course_id
                },
                headers: {
                    "Authorization": "jwt " + token
                },
            }).then(
                res => {
                    console.log(res.data.message)
                    this.$store.commit('add_cart', res.data.cart_len)
                    this.$emit('del_course')
                }
            ).catch(
                error => {
                    console.log(error)
                }
            )

        },
        change_status() {
            let token = this.check_user_login()
            this.$axios({
                url: this.$settings.HOST + 'cart/option/',
                method: "patch",
                data: {
                    course_id: this.course_id
                },
                headers: {
                    "Authorization": "jwt " + token
                }
            }).then(
                res => {
                    this.$emit('expire', 'dew')
                }
            ).catch(
                error => {
                    console.log(error);
                }
            )
        },
        change_expire() {
            let token = this.check_user_login()
            this.expire_time = this.course.expire_id
            this.$axios({
                url: this.$settings.HOST + 'cart/option/',
                method: "put",
                data: {
                    course_id: this.course.id,
                    expire_id: this.expire_time
                },
                headers: {
                    "Authorization": "jwt " + token
                }
            }).then(
                res => {
                    console.log(res.data.message)
                    this.$emit('expire', 'dew')
                }
            ).catch(
                error => {
                    console.log(error)
                }
            )
        }
    },
    props: ['course', 'checked'],
    watch: {
        "course.selected": function () {
            this.change_status()
        },
        "course.expire_id": function () {
            this.change_expire()
        },
        checked() {
            this.course.selected = this.checked
        }
    }
}
</script>

<style scoped>
.cart_item::after {
    content: "";
    display: block;
    clear: both;
}

.cart_column {
    float: left;
    height: 250px;
}

.cart_item .column_1 {
    width: 88px;
    position: relative;
}

.my_el_checkbox {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: 0;
    margin: auto;
    width: 16px;
    height: 16px;
}

.cart_item .column_2 {
    padding: 67px 10px;
    width: 520px;
    height: 116px;
}

.cart_item .column_2 img {
    width: 175px;
    height: 115px;
    margin-right: 35px;
    vertical-align: middle;
}

.cart_item .column_3 {
    width: 197px;
    position: relative;
    padding-left: 10px;
}

.my_el_select {
    width: 117px;
    height: 28px;
    position: absolute;
    top: 0;
    bottom: 0;
    margin: auto;
}

.cart_item .column_4 {
    padding: 67px 10px;
    height: 116px;
    width: 142px;
    line-height: 116px;
}
</style>
