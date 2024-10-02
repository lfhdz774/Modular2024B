
export class UserModel {
    constructor(username, password, email, first_name, last_name, employee_code, role, position_id) {
        this.username = username;
        this.password = password;
        this.email = email;
        this.first_name = first_name;
        this.last_name = last_name;
        this.employee_code = employee_code;
        this.role = role;
        this.employee_position = position_id;

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
            role: this.role,
            employee_position: this.employee_position
        };
    }
}