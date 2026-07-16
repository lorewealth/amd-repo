export const jwtPayload = (token) => JSON.parse(atob(token.split('.')[1]))
