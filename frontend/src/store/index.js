import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from '../router'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user_id: localStorage.getItem('user_id') || null,
    token: localStorage.getItem('token') || null,
    venue_id: localStorage.getItem('venue_id') || null
  },
  getters: {
    USER_ID(state) {
      return state.user_id
    },
    TOKEN(state) {
      return state.token
    },
    VENUE_ID(state) {
      return state.venue_id
    },
    IS_AUTHENTICATED(state) {
      return !!state.token
    }
  },
  mutations: {
    SIGNUP_MUTATION(state, payload) {
      state.token = payload.response.data.token
      state.user_id = payload.user_id
    },
    LOGIN_MUTATION(state, payload) {
      console.log(payload)
      state.token = payload.response.data.token
      state.user_id = payload.user_id
    },
    LOGOUT_MUTATION(state) {
      state.token = null
      state.user_id = null
    },
    SET_VENUE(state, payload) {
      state.venue_id = payload
    }
  },
  actions: {
    async SIGNUP_ACTION({ commit }, payload) {
      console.log("payload")
      try {
        axios.post('http://127.0.0.1:5000/signup',
                {
                    email: payload.email,
                    username: payload.name,
                    password: payload.password
                }
            )
                .then((response) => {
                    console.log(response.data.message);
                    localStorage.setItem('token', response.data.token);
                    localStorage.setItem('admin', response.data.admin);
                    const user_id = JSON.parse(atob(response.data.token.split('.')[1])).u_id
                    localStorage.setItem('user_id', user_id)
                    router.push('/dashboard')
                    commit('SIGNUP_MUTATION', {response, user_id})
                }
                ).catch((error) => {
                    console.log(error)
                    if (error.response.status == 409) {
                      alert ("User already exists ")
                    }
            });
       
      } catch (error) {
        console.log(error)
      }
    },
    async LOGIN_ACTION({ commit }, payload) {
      try {
        axios.post('http://127.0.0.1:5000/login',
                {
                    email: payload.email,
                    password: payload.password
                }
            )
                .then((response) => {
                    console.log(response.data);
                    localStorage.setItem('token', response.data.token);
                    const user_id = JSON.parse(atob(response.data.token.split('.')[1])).u_id
                    localStorage.setItem('user_id', user_id)
                    if (response.data.admin) {
                      commit('LOGIN_MUTATION', {response, user_id})
                      localStorage.setItem('admin', response.data.admin);
                      router.push('/admin')
                    } 
                    else {
                      commit('LOGIN_MUTATION', {response, user_id})
                      router.push('/dashboard')
                    }
                }
                ).catch((error) => {
                    console.log(error);
                     if (error.response.status == 401) {
                      alert ("Invalid password")
                    }
                    if (error.response.status == 404) {
                      alert ("Invalid email")
                    }
            });
       
      } catch (error) {
        console.log(error)
      }
      
    },
    LOGOUT_ACTION({ commit }) {
      commit('LOGOUT_MUTATION')
      localStorage.removeItem('token')
      localStorage.removeItem('user_id')
    },
    SET_VENUE_ACTION({ commit }, payload) {
      commit('SET_VENUE', payload)
      localStorage.setItem('venue_id', payload)
    }
  },
  modules: {
  }
})
