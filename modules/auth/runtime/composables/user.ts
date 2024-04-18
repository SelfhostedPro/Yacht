import type { User } from "../../types/user";

export const useUser = () => {
    const user = useState<User | null>("user", () => null);
    return user;
};