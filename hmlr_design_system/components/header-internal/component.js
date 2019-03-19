import React from 'react'

function Header(props) {

  const heading = props.homepageUrl ? (
    <p className="hmlr-header__title">
      <a href={props.homepageUrl} className='hmlr-header__link'>
        {props.headerTitle}
      </a>
    </p>
  ) : (
      <p className="hmlr-header__title">{props.headerTitle}</p>
    )

  return <header className='hmlr-header'>
    <div className='hmlr-header__inner'>
      {heading}
    </div>
  </header>
}

export default Header
