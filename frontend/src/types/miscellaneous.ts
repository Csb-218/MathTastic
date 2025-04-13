// Objective: Define the types for the miscellaneous data

export interface navItem {
  nav: string
  icon: string
  link: string
}

export interface DecodedToken {
  iat: number
  exp: number
  sub: {
    id: string
    name: string
    email: string
    role: string
    uid: string
  }
}

export interface DecodedIdToken {
  name: string
  email: string
  role: string
  uid: string
}
