import React from 'react'
import logoImage from './logo.svg'

function Header (props) {
  const Logo = (
    <img className='hmlr-header__logo'
      src={logoImage}
      alt='HM Land Registry' />
  )

  return <header className='hmlr-header'>
    <div className='hmlr-header__inner'>
      { props.homepageUrl
        ? (
          <a href={props.homepageUrl} className='hmlr-header__link'>
            Logo
          </a>
        ) : (
          Logo
        )
      }
    </div>
  </header>
}

export default Header
