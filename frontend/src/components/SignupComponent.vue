<template>
    <b-container>
        <div>
            <b-form class="form" @submit="onSubmit" @reset="onReset">
                <b-form-group id="input-group-1" label-for="input-1">
                    <b-form-input class="inp" id="input-1" v-model="form.email" type="email" placeholder="Enter email"
                        required></b-form-input>
                </b-form-group>

                <b-form-group id="input-group-2" label-for="input-2">
                    <b-form-input class="inp" id="input-2" v-model="form.name" placeholder="Enter Name"
                        required></b-form-input>
                </b-form-group>

                <b-form-group id="input-group-3" label-for="input-3" :state="passwordValidationState">
                    <div class="password-input">
                        <b-form-input class="inp" :type="showPassword ? 'text' : 'password'" id="input-3"
                            v-model="form.password" placeholder="Type Password" required
                            @input="validatePassword"></b-form-input>
                        <span class="password-toggle" @click="togglePasswordVisibility">
                            <i :class="['fas', showPassword ? 'fa-eye-slash' : 'fa-eye']"></i>
                        </span>
                    </div>
                    <div class="password-feedback">
                        <b-popover v-if="!isStrongPassword()" target="input-3" triggers="hover focus" placement="top">
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

                <b-form-group id="input-group-4" label-for="input-4" :state="confirmPasswordValidationState">
              <b-form-input class="inp" type="password" id="input-4" v-model="confirmPassword" placeholder="Confirm Password" required
                @input="validateConfirmPassword"></b-form-input>
              <b-popover v-if="showPasswordMismatchPopover" target="input-4" triggers="hover focus" placement="top" variant="danger" auto-hide="false">
                Passwords do not match
              </b-popover>
              <b-form-valid-feedback>
                <template v-if="confirmPassword === form.password">Passwords match</template>
              </b-form-valid-feedback>
            </b-form-group>

                <b-button type="submit" pill class="but mr-2">SignUp</b-button>
                <b-button type="reset" pill class="but">Reset</b-button>
                <br>
                <br>
                <a style="color: white;" @click="toggle">Already Have An Account?</a>
                <b-button @click="toggle" pill class="but ml-2">Login</b-button>
            </b-form>
        </div>
    </b-container>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    data() {
        return {
            form: {
                email: '',
                name: '',
                password: '',
            },
            confirmPassword: '',
            show: true,
            showPassword: false,
            isAtLeast8Chars: false,
            hasUppercase: false,
            hasLowercase: false,
            hasDigit: false,
            hasSpecialChar: false,
            showPasswordMismatchPopover: false,
        };
    },
    computed: {
        passwordValidationState() {
            return this.form.password && this.isStrongPassword() ? 'valid' : 'invalid';
        },
        confirmPasswordValidationState() {
            return this.confirmPassword === this.form.password ? 'valid' : 'invalid';
        },
    },
    methods: {
        ...mapActions({
            signup: 'SIGNUP_ACTION',
        }),
        onSubmit(event) {
            event.preventDefault();
            if (this.form.password !== this.confirmPassword) {
                this.showPasswordMismatchPopover = true;
                return;
            } else {
                this.showPasswordMismatchPopover = false;
            }

            this.signup(this.form);
        },
        onReset(event) {
            event.preventDefault();
            // Reset our form values
            this.form.email = '';
            this.form.name = '';
            this.form.password = '';
            this.confirmPassword = '';
            this.isAtLeast8Chars = false;
            this.hasUppercase = false;
            this.hasLowercase = false;
            this.hasDigit = false;
            this.hasSpecialChar = false;
            this.showPasswordMismatchPopover = false;
        },
        toggle() {
            this.$emit('toggle-event');
        },
        validatePassword() {
            this.isAtLeast8Chars = this.form.password.length >= 8;
            this.hasUppercase = /[A-Z]/.test(this.form.password);
            this.hasLowercase = /[a-z]/.test(this.form.password);
            this.hasDigit = /\d/.test(this.form.password);
            this.hasSpecialChar = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]+/.test(this.form.password);
        },
        isStrongPassword() {
            return (
                this.isAtLeast8Chars &&
                this.hasUppercase &&
                this.hasLowercase &&
                this.hasDigit &&
                this.hasSpecialChar
            );
        },
        togglePasswordVisibility() {
            this.showPassword = !this.showPassword;
        },
        validateConfirmPassword() {
            this.showPasswordMismatchPopover = this.confirmPassword !== this.form.password;
        },
    },
};
</script>

<style scoped>
.inp {
    background-color: transparent;
    color: white;
    border-color: transparent;
    box-shadow: inset 20px 20px 23px #1e1e1e, inset -20px -20px 23px #2e2e2e;
}

.form {
    max-width: auto;
    max-height: auto;
    margin-bottom: 90%;
    padding: 50px 30px;
    border-radius: 5px;
    backdrop-filter: blur(7px);
    box-shadow: rgba(0, 0, 0, 0.867) 13px 39px 88px;
}

.but {
    background: #838181;
    box-shadow: inset 17px 17px 35px #555454, inset -17px -17px 35px #b1aeae;
}

.password-input {
    position: relative;
    display: flex;
    align-items: center;
}

.password-toggle {
    position: absolute;
    right: 10px;
    cursor: pointer;
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
}

.password-feedback {
    margin-top: 5px;
}</style>
