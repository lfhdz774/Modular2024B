export function getUserRoles() {
    const storedRoles = localStorage.getItem('user_role');
    return storedRoles ? JSON.parse(storedRoles) : [];
  }