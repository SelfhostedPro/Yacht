import type { YachtConfig } from "../../types"

export const useClientConfig = () => {
    const clientConfig = useState<Pick<YachtConfig, 'auth' | 'theme'> | null>("auth-enabled", () => null)
    return clientConfig
}