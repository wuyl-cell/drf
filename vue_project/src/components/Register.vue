<template>
    <div class="box">
        <img src="../../static/image/1111.jpg" alt="">
        <div class="register">
            <div class="register_box">
                <div class="register-title">百知教育在线平台注册</div>
                <div class="inp">
                    <input v-model="mobile" type="text" placeholder="手机号码" class="user" @blur="check_mobile">
                    <input v-model="password" type="password" placeholder="登录密码" class="user" @blur="check_password">
                    <div id="geetest"></div>
                    <div class="sms-box">
                        <input v-model="code" type="text" maxlength="6" placeholder="输入验证码" class="user" >
                        <div class="sms-btn" @click="send_code" v-if="is_show">发送验证码</div>
                        <div class="sms-btn" v-else>{{ count }}s后重新发送</div>
                    </div>
                    <button class="register_btn" @click="user_register">注册</button>
                    <p class="go_login">已有账号
                        <!--                        <router-link to="/login">直接登录</router-link>-->
                        <router-link to="/login">直接登录</router-link>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Register",
    data(){
        return{
            mobile: '',
            password: '',
            code: '',
            mobile_check: false,
            password_check: false,
            count: '',
            is_show: true,
            timer: null,
        }
    },
    methods: {
        check_mobile(){
            let phone=/^[1][3,4,5,7,8][0-9]{9}$/;
            if (phone.test(this.mobile)){
                this.$axios({
                    url: this.$settings.HOST + 'user/phone_register/',
                    method: "get",
                    params: {
                        phone: this.mobile
                    }
                }).then(
                    res => {
                        this.mobile_check = true
                    }
                ).catch(
                    error => {
                        console.log(error)
                        this.mobile_check = false
                        this.$message({
                            message: error.response.data.message,
                            type: 'warning',
                            duration: 1000,
                        })
                    }
                )
            }
            else {
                this.mobile_check = false
                this.$message( {
                    message: '手机号格式错误',
                    type: 'warning',
                    duration: 1000,
                })
            }
        },
        user_register(){
            if(this.mobile_check && this.password_check){
                this.$axios({
                    url: this.$settings.HOST + 'user/register/',
                    method: "post",
                    data: {
                        phone: this.mobile,
                        password: this.password,
                        code: this.code
                    }
                }).then(
                    res => {
                        // 保存用户登陆状态
                        sessionStorage.token = res.data.token
                        this.$message( {
                            message: '恭喜你，注册成功并自动登陆',
                            type: 'success',
                            duration: 1000,
                        })
                        // 跳转到主页
                        this.$router.push('/home')

                    }
                ).catch(
                    error => {
                        this.$message( {
                            message: '验证码错误',
                            type: 'warning',
                            duration: 1000,
                        })
                    }
                )
            }
            else if ( !this.mobile_check ){
                this.$message( {
                    message: '手机号不符合要求',
                    type: 'warning',
                    duration: 1000,
                })
            }
            else {
                this.$message( {
                    message: '密码不符合要求',
                    type: 'warning',
                    duration: 1000,
                })
            }

        },
        send_code(){
            const TIME_COUNT = 60;
            if(this.mobile_check){
                this.$axios({
                    url: this.$settings.HOST + 'user/get_code/',
                    method: "get",
                    params: {
                        phone: this.mobile
                }
                }).then(
                    res => {
                        this.$message({
                            message: res.data,
                            type: 'seccess',
                            duration: 1000,
                        })
                        this.count = TIME_COUNT;
                        this.is_show = false;
                        this.timer = setInterval(() => {
                            if (this.count > 0 && this.count <= TIME_COUNT){
                                this.count --;
                            }
                            else{
                                this.is_show = true;
                                clearInterval(this.timer);
                                this.timer = null;
                            }
                        }, 1000)
                    }
                ).catch(
                    error => {
                        this.$message({
                            message: error.response.data.message,
                            type: 'waring',
                            duration: 1000,
                        })
                    }
                )
            }
            else{
                this.$message({
                    message: '请输入正确的手机号',
                    type: 'waring',
                    duration: 1000,
                })
            }
        },

        check_password(){
            let num =  /^[0-9]+$/
            let digit = /^[a-zA-Z]+$/
            let is_num = num.test(this.password)
            let is_digit = digit.test(this.password)
            if(this.password.length>=6 && !is_num && !is_digit){
                this.password_check = true
            }
            else if(this.password.length<6){
                this.password_check = false
                this.$message({
                    message: '密码长度不能小于6位',
                    type: 'seccess',
                    duration: 1000,
                })
            }
            else{
                this.password_check = false
                this.$message({
                    message: '密码必须是数字和字母的组合',
                    type: 'seccess',
                    duration: 1000,
                })
            }

        },
    },
}
</script>

<style scoped>
.box {
    width: 100%;
    height: 100%;
    position: relative;
    overflow: hidden;
}

.box img {
    width: 100%;
    min-height: 100%;
}

.box .register {
    position: absolute;
    width: 500px;
    height: 400px;
    top: 0;
    left: 0;
    margin: auto;
    right: 0;
    bottom: 0;
    top: -338px;
}

.register .register-title {
    width: 100%;
    font-size: 24px;
    text-align: center;
    padding-top: 30px;
    padding-bottom: 30px;
    color: #4a4a4a;
    letter-spacing: .39px;
}

.register-title img {
    width: 190px;
    height: auto;
}

.register-title p {
    font-family: PingFangSC-Regular;
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
}

.register_box {
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
}

.register_box .title {
    font-size: 20px;
    color: #9b9b9b;
    letter-spacing: .32px;
    border-bottom: 1px solid #e6e6e6;
    display: flex;
    justify-content: space-around;
    padding: 50px 60px 0 60px;
    margin-bottom: 20px;
    cursor: pointer;
}

.register_box .title span:nth-of-type(1) {
    color: #4a4a4a;
    border-bottom: 2px solid #84cc39;
}

.inp {
    width: 350px;
    margin: 0 auto;
}

.inp input {
    border: 0;
    outline: 0;
    width: 100%;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}

.inp input.user {
    margin-bottom: 16px;
}

.inp .rember {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 10px;
}

.inp .rember p:first-of-type {
    font-size: 12px;
    color: #4a4a4a;
    letter-spacing: .19px;
    margin-left: 22px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    /*position: relative;*/
}

.inp .rember p:nth-of-type(2) {
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
    cursor: pointer;
}

.inp .rember input {
    outline: 0;
    width: 30px;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}

.inp .rember p span {
    display: inline-block;
    font-size: 12px;
    width: 100px;
    /*position: absolute;*/
    /*left: 20px;*/

}

#geetest {
    margin-top: 20px;
}

.register_btn {
    width: 100%;
    height: 45px;
    background: #84cc39;
    border-radius: 5px;
    font-size: 16px;
    color: #fff;
    letter-spacing: .26px;
    margin-top: 30px;
}

.inp .go_login {
    text-align: center;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .26px;
    padding-top: 20px;
}

.inp .go_login span {
    color: #84cc39;
    cursor: pointer;
}

.sms-box {
    position: relative;
}

.sms-btn {
    font-size: 14px;
    color: #ffc210;
    letter-spacing: .26px;
    position: absolute;
    right: 16px;
    top: 10px;
    cursor: pointer;
    overflow: hidden;
    background: #fff;
    border-left: 1px solid #484848;
    padding-left: 16px;
    padding-bottom: 4px;
}
</style>
