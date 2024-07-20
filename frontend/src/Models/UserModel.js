
export class UserModel {
    constructor(username, password, email, firstName, lastName, employeeCode, roleId) {
        this.user_id = null; // Inicializar en null, se asignará por el backend
        this.username = username;
        this.password = password;
        this.email = email;
        this.first_name = firstName;
        this.last_name = lastName;
        this.employee_code = employeeCode;
        this.role_id = roleId;
    }

    toJSON() {
        return {
            user_id: this.user_id,
            username: this.username,
            // ... puedes incluir otras propiedades si es necesario
        };
    }
}