Vue.createApp({
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        return {
            RegSchema: {
                reg: (value) => {
                    if (value) {
                        return true;
                    }
                    return 'Поле не заполнено';
                },
                phone_format: (value) => {
                    const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат телефона нарушен';
                    }
                    return true;
                },
                code_format: (value) => {
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
            Step: 'Number',
            RegInput: '',
            EnteredNumber: '',
            PhoneNumber: '',
            Code: ''
        }
    },
    methods: {
        RegSubmit() {
            if (this.Step === 'Number') {
                // this.$refs.HiddenFormSubmitPhone.click()
                this.Step = 'Code'
                this.PhoneNumber = this.RegInput
                axios.get('phone/', {params: {phone_number: this.PhoneNumber}})
                this.RegInput = ''
            }
            else if (this.Step === 'Code') {
                this.Code = this.RegInput
                this.$refs.HiddenFormSubmitPhone.click()
                // axios.get('login/', {params: {phone_number: this.PhoneNumber, code: this.RegInput}})
                this.Step = 'Finish'
                this.RegInput = 'Регистрация успешна'
            }
        },
        ToRegStep1() {
            this.Step = 'Number'
            this.RegInput = this.EnteredNumber
        },
        Reset() {
            this.Step = 'Number'
            this.RegInput = ''
            EnteredNumber = ''
        }
    }
}).mount('#RegModal')