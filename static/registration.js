Vue.createApp({
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        return {
            RegSchema: {
                phone: (value) => {
                    if (this.regFormField.name !== 'phone') {
                        return true
                    }

                    if (!value) {
                        return 'Поле не заполнено';
                    }

                    const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат телефона нарушен';
                    }
                    return true;
                },
                code: (value) => {
                    if (this.regFormField.name !== 'code') {
                        return true
                    }

                    if (!value) {
                        return 'Поле не заполнено';
                    }

                    const regex = /^[a-zA-Z0-9]+$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат кода нарушен';
                    }
                    return true;
                }
            },
            regFormState: 'phone',
            RegInput: '',
            PhoneNumber: '',
            Code: '',
            isLoading: false
        }
    },
    methods: {
        async RegSubmit() {
            if (this.regFormState === 'phone') {
                this.regFormState = 'code'
                this.PhoneNumber = this.RegInput
                this.isLoading = true
                const response = await axios.get('phone/', {params: {phone_number: this.PhoneNumber}})
                this.isLoading = false
                this.RegInput = ''
            } else if (this.regFormState === 'code') {
                this.Code = this.RegInput
                this.isLoading = true
                await axios.get('login/', {params: {phone_number: this.PhoneNumber, code: this.RegInput}})
                this.isLoading = false
                this.regFormState = 'finished'
                this.RegInput = ''
                this.$refs.resetButton.click()
                location.reload()
            }
        },
        Reset() {
            this.regFormState = 'phone'
            this.RegInput = ''
        }
    },
    computed: {
        regFormField() {
            return {
                isFinished: this.regFormState === 'finished',
                placeholder: this.regFormState === `phone` ? `Введите ваш номер` : `Введите код`,
                name: this.regFormState,
                info: {
                    code: 'Осталось времени: 05:00',
                    phone: 'Нажимая на кнопку, вы соглашаетесь на обработку персональных данных в соответствии с политикой конфиденциальности'
                }[this.regFormState]
            }
        }
    }
}).mount('#RegModal')