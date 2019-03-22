import React from 'react'

function HeaderInternal(props) {

  const heading = props.homepageUrl ? (
    <p className="hmlr-header__title">
      <a href={props.homepageUrl} className='hmlr-header__link'>
        {props.headerTitle}
      </a>
    </p>
  ) : (
      <p className="hmlr-header__title">{props.headerTitle}</p>
    )

  return <header className='hmlr-header--internal'>
    <div className={`hmlr-header__inner ${props.innerClasses}`}>
      {heading}
    </div>
  </header>
}

export default HeaderInternal
