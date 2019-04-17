import React from 'react'

function HeaderInternal(props) {

  const heading = props.homepageUrl ? (
    <p className="hmlr-header-internal__title">
      <a href={props.homepageUrl} className='hmlr-header__link'>
        {props.headerTitle}
      </a>
    </p>
  ) : (
      <p className="hmlr-header-internal__title">{props.headerTitle}</p>
    )

  return <header className='hmlr-header-internal'>
    <div className={`hmlr-header-internal__inner ${props.innerClasses}`}>
      {heading}
    </div>
  </header>
}

export default HeaderInternal
