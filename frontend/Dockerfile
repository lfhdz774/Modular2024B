# Step 1: Use a Node.js base image
FROM node:14

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the package.json and package-lock.json files
COPY package*.json ./

# Step 4: Install dependencies
RUN npm install

# Step 5: Copy the rest of the app files
COPY . .

# Step 6: Expose the port the app will run on
EXPOSE 3000

# Step 7: Start the React app in development mode
CMD ["npm", "start"]