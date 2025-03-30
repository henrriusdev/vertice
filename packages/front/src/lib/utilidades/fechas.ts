export const now = () => new Date();

export const maxYearDate = () => new Date(now().getFullYear() - 16, now().getMonth(), now().getDate());