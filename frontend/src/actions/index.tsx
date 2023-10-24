export const save_user = (user:any) => {
    return {
        type: 'SIGN_IN',
        payload: user
    }
}