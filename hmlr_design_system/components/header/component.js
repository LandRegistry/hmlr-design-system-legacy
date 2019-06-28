import React from 'react'
import PropTypes from 'prop-types'
import logoImage from './logo.png'
import whiteLogoImage from './logo-white.png'

function Header(props) {
  let logo

  if (props.variant === 'dark') {
    logo = <img className="hmlr-header__logo" width="103px" height="32px" src={whiteLogoImage} alt="HM Land Registry" />
  } else {
    logo = <img className="hmlr-header__logo" width="233px" height="72px" src={logoImage} alt="HM Land Registry" />
  }

  const headerTitle = props.headerTitle && <span className="hmlr-header__title">{props.headerTitle}</span>

  const contents = <>
    {props.logo && logo}
    {headerTitle}
  </>

  return <header className={`hmlr-header hmlr-header--${props.variant} ${props.classes}`}>
    <div className="hmlr-header__inner">
      {props.homepageUrl
        ? (
          <a href={props.homepageUrl} className="hmlr-header__link">
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
  variant: 'white',
}

Header.propTypes = {
  variant: PropTypes.string,
  classes: PropTypes.string,
  headerTitle: PropTypes.node,
  logo: PropTypes.bool,
  homepageUrl: PropTypes.string,
}

export default Header
