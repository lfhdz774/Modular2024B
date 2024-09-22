class Command {
    constructor(commandId, comando, createdAt, updatedAt, userId) {
      this.commandId = commandId;
      this.comando = comando;
      this.createdAt = createdAt;
      this.updatedAt = updatedAt;
      this.userId = userId;
    }
  }
  
  export default Command;