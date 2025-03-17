export type user = {
    name: string,
    email: string,
    uid: string,
    role: "admin" | "student" | "educator"
}

export type user_state = {
    name: string
    session: string
    email: string
    role: string
}

export type login = {
    email: string,
    uid: string,
}