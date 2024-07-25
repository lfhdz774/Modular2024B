
export class UserModel {
    constructor(username, password, email, first_name, last_name, employee_code, role) {
        this.username = username;
        this.password = password;
        this.email = email;
        this.first_name = first_name;
        this.last_name = last_name;
        this.employee_code = employee_code;
        this.role = role;
    }


    toJSON() {
        return {
            user_id: this.user_id,
            username: this.username,
            password: this.password,
            email: this.email,
            first_name: this.first_name,
            last_name: this.last_name,
            employee_code: this.employee_code,
            role: this.role
        };
    }
}