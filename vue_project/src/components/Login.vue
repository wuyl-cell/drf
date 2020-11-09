<template>
    <div class="login box">
        <img src="../../static/image/1111.jpg" alt="">
        <div class="login">
            <div class="login-title">
                <img src="../../static/image/logo.png" alt="">
                <p>百知教育给你最优质的学习体验!</p>
            </div>
            <div class="login_box">
                <div class="title">
                    <span @click="change_name" v-show="is_show">密码登录</span>
                    <span @click="change_name" v-show="!is_show">密码登录</span>
                    <span @click="change_message" v-show="is_show">短信登录</span>
                    <span @click="change_message" v-show="!is_show">短信登录</span>
                </div>

                <div class="inp" v-if="is_show">
                    <input type="text" placeholder="用户名 / 手机号码" class="user" v-model="username">
                    <input type="password" name="" class="pwd" placeholder="密码" v-model="password">
                    <div id="geetest1"></div>
                    <div class="rember">
                        <p>
                            <input type="checkbox" class="no" />
                            <span>记住密码</span>
                        </p>
                        <p>忘记密码</p>
                    </div>
                    <button class="login_btn btn btn-primary" @click="get_captcha" v-bind:disabled="dis">登录</button>
                    <p class="go_login">没有账号
                        <router-link to="/register/">立即注册</router-link>
                    </p>
                </div>
                <div class="inp" v-else>
                    <input type="text" placeholder="手机号码" class="user" v-model="mobile" @blur="check_mobile">

                    <input type="text" class="pwd" placeholder="短信验证码" v-model="code">
                    <div class="rember">
                        <p>
                            <button id="get_code1" class="btn btn-primary" @click="send_code" v-if="show">获取验证码</button>
                            <button id="get_code2" class="btn btn-primary" v-else>{{ count }}s后重新发送</button>
                        </p>
                    </div>

                    <button class="login_btn" @click="message_login">登录</button>
                    <p class="go_login">没有账号
                        <router-link to="/register/">立即注册</router-link>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Login",
    data(){
        return {
            username: '',
            password: '',
            mobile: '',
            is_show: true,
            mobile_check: false,
            dis: false,
            code: '',
            count: '',
            show: true,
            timer: null,
        }
    },
    methods:{
        handlerPopup(captchaObj) {
            let self = this;
            captchaObj.onSuccess(function () {
                let validate = captchaObj.getValidate();
                self.$axios({
                    url: self.$settings.HOST + "user/captcha/",
                    method: "post",
                    data: {
                        geetest_challenge: validate.geetest_challenge,
                        geetest_validate: validate.geetest_validate,
                        geetest_seccode: validate.geetest_seccode
                    },
                }).then(response => {
                    self.user_login()
                }).catch(error =>{
                });
            });
            // 将验证码加到id为captcha的元素里
            document.getElementById('geetest1').innerHTML = ''
            captchaObj.appendTo("#geetest1");
        },
        get_captcha(){
            if (this.username && this.password){
                this.$axios({
                    url: this.$settings.HOST + 'user/captcha/',
                    method: "get",
                    params: {
                        username: this.username
                    },
                }).then(
                    response => {
                        let data = JSON.parse(response.data);
                        initGeetest({
                            gt: data.gt,
                            challenge: data.challenge,
                            product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
                            offline: !data.success, // 表示用户后台检测极验服务器是否宕机，一般不需要关注
                            new_captcha: data.new_captcha
                        }, this.handlerPopup);
                    }
                ).catch(error => {
                    this.$message( {
                        message: error.response.data.message,
                        type: 'warning',
                        duration: 1000,
                    })

                });
            }
            else{
                this.$message( {
                    message: '请输入用户名和密码',
                    type: 'warning',
                    duration: 1000,
                })
            }

        },
        user_login(){
            this.$axios({
                url: this.$settings.HOST + 'user/login/',
                method: "post",
                data: {
                    username: this.username,
                    password: this.password,
                }
            }).then(
                response => {
                    if (response.data){
                        this.$message( {
                            message: '恭喜你，登陆成功',
                            type: 'success',
                            duration: 1000,
                        })
                    }
                    sessionStorage.token = response.data.token
                    this.$router.push('/home')
                }
            ).catch(error => { console.log(error);

            })

        },
        change_message(){
            this.is_show = false
        },
        change_name(){
            this.is_show = true
        },
        check_mobile(){
            let phone=/^[1][3,4,5,7,8][0-9]{9}$/;
            if (phone.test(this.mobile)){
                this.$axios({
                    url: this.$settings.HOST + 'user/phone_login/',
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
        send_code(){
            if(this.mobile_check){
                const TIME_COUNT = 60;
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
                        this.show = false;
                        this.timer = setInterval(() => {
                            if (this.count > 0 && this.count <= TIME_COUNT){
                                this.count --;
                            }
                            else{
                                this.show = true;
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
        message_login(){
            this.$axios({
                url: this.$settings.HOST + 'user/message_login/',
                method: "get",
                params: {
                    code: this.code,
                    phone: this.mobile
                }
            }).then(
                res => {
                    this.$message({
                        message: '恭喜你，登陆成功！',
                        type: 'seccess',
                        duration: 1000,
                    })
                    sessionStorage['token'] = res.data.token
                    this.$router.push('/')
                }
            ).catch(
                error => {
                    this.$message({
                        message: error.response.data.message,
                        type: 'warning',
                        duration: 1000,
                    })
                }
            )
        }

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

.box .login {
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

.login .login-title {
    width: 100%;
    text-align: center;
}

.login-title img {
    width: 190px;
    height: auto;
}

.login-title p {
    font-family: PingFangSC-Regular;
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
}

.login_box {
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
}

.login_box .title {
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

.login_box .title span:nth-of-type(1) {
    color: #4a4a4a;
    border-bottom: 2px solid #84cc39;
}

.login_box .title span:nth-of-type(4) {
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

.login_btn {
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
</style>
