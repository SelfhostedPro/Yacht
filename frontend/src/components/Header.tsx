import YachtLogo from "../icons/YachtLogo"
import { User } from "../utils"

interface OwnProps {
  user: User
}

const Header = ({user}: OwnProps) => {
  return (
    <div className={'flex flex-row justify-between p-4 text-white font-bold'} style={{height: '64px', backgroundColor: '#424242'}}>
      <div className={'flex flex-row'}><YachtLogo/> Yacht</div>
      <span>Home</span>
      <div>{user.username}</div>
    </div>
  )
}

export default Header
g