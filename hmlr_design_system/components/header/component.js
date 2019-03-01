import React from 'react'

function Header (props) {
  const Logo = (

    // TODO: Consider paths to images. React way would be to use file-loader
    // Just do it twice?!

    <img className='hmlr-header__logo'
      src={`${window.application_config.static_path}images/hmlr-hmlr-design-system/header/logo.svg`}
      alt='HM Land Registry' />
  )

  return <>
    <header className='hmlr-header'>
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
  </>
}

export default Header
