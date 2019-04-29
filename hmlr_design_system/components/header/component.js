import React from 'react'
import logoImage from './logo.png'
import whiteLogoImage from './logo-white.png'

function Header(props) {
  var logo

  if (props.variant === 'dark') {
    logo = <img className='hmlr-header__logo' width='87px' height='29px' src={whiteLogoImage} alt='HM Land Registry' />
  } else {
    logo = <img className='hmlr-header__logo' width='162px' height='50px' src={logoImage} alt='HM Land Registry' />
  }

  const headerTitle = props.headerTitle && <span className="hmlr-header__title">{props.headerTitle}</span>

  const contents = <>
    {props.logo && logo}
    {headerTitle}
  </>

  return <header className={`hmlr-header hmlr-header--${props.variant} ${props.classes}`}>
    <div className='hmlr-header__inner'>
      {props.homepageUrl
        ? (
          <a href={props.homepageUrl} className='hmlr-header__link'>
            contents
          </a>
        ) : (
          contents
        )
      }
    </div>
  </header>
}

Header.defaultProps = {
  variant: 'white'
}

export default Header
