<template>
    <div class="container">
        <div style="color: transparent; background-color: transparent;">
            <b-form class="form" @submit="onSubmit" @reset="onReset" v-if="show">
                <!-- Email Input Field -->
                <b-form-group id="input-group-1" label="Email address:" label-for="input-1"
                    description="We'll never share your email with anyone else." :state="emailValidationState">
                    <b-form-input class="inp" id="input-1" v-model="form.email" type="email" placeholder="Enter email"
                        required @input="validateEmail"></b-form-input>
                    <small class="text-danger" v-if="emailValidationState === false">Invalid email format</small>
                </b-form-group>

                <!-- Password Input Field -->
                <b-form-group id="input-group-2" label="Your Password:" label-for="input-2"
                    :state="passwordValidationState">
                    <div class="password-input">
                        <b-form-input class="inp" :type="showPassword ? 'text' : 'password'" id="input-2"
                            v-model="form.password" placeholder="Enter password" required
                            @input="validatePassword"></b-form-input>
                        <span class="password-toggle" @click="togglePasswordVisibility">
                            <i :class="['fas', showPassword ? 'fa-eye-slash' : 'fa-eye']"></i>
                        </span>
                    </div>
                    <div class="password-feedback">
                        <b-popover v-if="!isStrongPassword()" target="input-2" triggers="hover" placement="top">
                            <template #title>Password Criteria</template>
                            <ul class="password-criteria">
                                <li :class="{ 'invalid': !isAtLeast8Chars }">At least 8 characters long</li>
                                <li :class="{ 'invalid': !hasUppercase }">At least one uppercase letter</li>
                                <li :class="{ 'invalid': !hasLowercase }">At least one lowercase letter</li>
                                <li :class="{ 'invalid': !hasDigit }">At least one digit</li>
                                <li :class="{ 'invalid': !hasSpecialChar }">At least one special character</li>
                            </ul>
                        </b-popover>
                    </div>
                </b-form-group>

                <!-- Submit and Reset Buttons -->
                <b-button type="submit" pill class="but mr-2">Login</b-button>
                <b-button type="reset" pill class="but">Reset</b-button>
                <br>
                <br>
                <a style="color: white;" @click="toggle">Don't Have An Account?</a>
                <b-button @click="toggle" pill class="but ml-2">SignUp</b-button>
            </b-form>
        </div>
    </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    data() {
        return {
            form: {
                email: '',
                password: ''
            },
            show: true,
            showPassword: false,
            isAtLeast8Chars: false,
            hasUppercase: false,
            hasLowercase: false,
            hasDigit: false,
            hasSpecialChar: false
        };
    },
    computed: {
        emailValidationState() {
            return this.form.email && this.isValidEmail(this.form.email);
        },
        passwordValidationState() {
            return this.form.password && this.isStrongPassword();
        }
    },
    methods: {
        ...mapActions({
            login: 'LOGIN_ACTION'
        }),

        validateEmail() {
            this.emailValidationState = this.isValidEmail(this.form.email);
        },
        validatePassword() {
            this.isAtLeast8Chars = this.form.password.length >= 8;
            this.hasUppercase = /[A-Z]/.test(this.form.password);
            this.hasLowercase = /[a-z]/.test(this.form.password);
            this.hasDigit = /\d/.test(this.form.password);
            this.hasSpecialChar = /[!@#$%^&*()_+{}[\]:;<>,.?~\\/-]/.test(this.form.password);
            this.passwordValidationState = this.isStrongPassword();
        },
        isStrongPassword() {
            return this.isAtLeast8Chars && this.hasUppercase && this.hasLowercase && this.hasDigit && this.hasSpecialChar;
        },
        togglePasswordVisibility() {
            this.showPassword = !this.showPassword;
        },
        onSubmit(event) {
            event.preventDefault();
            if (this.form.email==="admin@email.com" && this.form.password==="admin") {
                this.login(this.form);
            }
            if (this.emailValidationState && this.passwordValidationState) {
                // Perform login action here
                this.login(this.form);
                console.log('Form submitted');
            }
        },
        onReset(event) {
            event.preventDefault();
            // Reset form and validation states
            this.form.email = '';
            this.form.password = '';
            this.isAtLeast8Chars = false;
            this.hasUppercase = false;
            this.hasLowercase = false;
            this.hasDigit = false;
            this.hasSpecialChar = false;
        },
        toggle() {
            this.$emit('toggle-event');
        },
        isValidEmail(email) {
            // Email validation logic here
            return /\S+@\S+\.\S+/.test(email);
        }
    }
};
</script>

<style scoped>
.inp {
    background-color: transparent;
    color: white;
    border-color: transparent;
    box-shadow: inset 20px 20px 23px #1e1e1e,
        inset -20px -20px 23px #2e2e2e;
}

.form {
    max-width: auto;
    max-height: auto;
    margin-bottom: 90%;
    padding: 30px 20px;
    border-radius: 5px;
    backdrop-filter: blur(7px);
    box-shadow: rgba(0, 0, 0, 0.867) 13px 39px 88px;
}

.but {
    background: #838181;
    box-shadow: inset 17px 17px 35px #555454,
        inset -17px -17px 35px #b1aeae;
}


.password-feedback {
    margin-top: 0.5rem;
}

.password-input {
    display: flex;
    align-items: center;
}

.password-toggle {
    cursor: pointer;
    margin-left: -25px;
    font-size: 1.25rem;
    color: #999;
}

.password-toggle i:hover {
    color: #333;
}

.password-criteria {
    list-style: none;
    padding-left: 1rem;
}

.password-criteria li {
    margin-bottom: 0.25rem;
    font-weight: bold;
}

.password-criteria .invalid {
    color: #d9534f;
    /* Red color for invalid criteria */
}
</style>
